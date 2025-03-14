package com.example.OmniTrack.websocket;

import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.socket.BinaryMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.AbstractWebSocketHandler;
import org.springframework.web.socket.TextMessage;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.client.RestTemplate;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.*;
import java.io.IOException;

@Component
public class VideoStreamHandler extends AbstractWebSocketHandler {

    private static final String CLIP_API_URL = "http://127.0.0.1:8000/predict";
    private volatile long lastResetTimestamp = 0;
    private static final long RESET_COOLDOWN_MS = 1000;
    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        System.out.println("WebSocket connection established with session id: " + session.getId());
    }
    @Override
    protected void handleBinaryMessage(WebSocketSession session, BinaryMessage message) throws Exception {
        long currentTime = System.currentTimeMillis();
        if (currentTime < lastResetTimestamp + RESET_COOLDOWN_MS) {
            System.out.println("Frame ignored due to recent reset.");
            return;
        }
        System.out.println("Received binary message of size: " + message.getPayloadLength() + " bytes");
        String result = classifyFrame(message.getPayload().array());

        try {
            session.sendMessage(new TextMessage("CLIP Analysis: " + result));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception {
        String payload = message.getPayload();
        if (payload.equalsIgnoreCase("RESET")) {
            System.out.println("Received RESET command, resetting CLIP model state.");
            lastResetTimestamp = System.currentTimeMillis();
            session.sendMessage(new TextMessage("RESET_ACK"));
        } else {
            System.out.println("Received text message: " + payload);
        }
    }
    private String classifyFrame(byte[] frameData) {
        try {
            RestTemplate restTemplate = new RestTemplate();
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.MULTIPART_FORM_DATA);
            MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
            body.add("image", new ByteArrayResource(frameData) {
                @Override
                public String getFilename() {
                    return "frame.jpg";
                }
            });
            HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
            ResponseEntity<String> response = restTemplate.exchange(CLIP_API_URL, HttpMethod.POST, requestEntity, String.class);

            return response.getBody();
        } catch (Exception e) {
            e.printStackTrace();
            return "Error in CLIP classification";
        }
    }
    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        System.out.println("WebSocket connection closed with session id: " + session.getId());
    }
    @Override
    public void handleTransportError(WebSocketSession session, Throwable exception) throws Exception {
        System.out.println("Error during WebSocket communication: " + exception.getMessage());
    }
}
