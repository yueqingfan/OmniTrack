package com.example.OmniTrack.websocket;

import org.springframework.web.socket.BinaryMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.AbstractWebSocketHandler;
import org.springframework.web.socket.TextMessage;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import java.io.IOException;

@Component
public class VideoStreamHandler extends AbstractWebSocketHandler {

    // 当有客户端连接时调用
    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        System.out.println("WebSocket connection established with session id: " + session.getId());
    }

    // 处理客户端发送的文本消息
    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception {
        // 处理接收到的文本消息（如果需要）
        System.out.println("Received message: " + message.getPayload());

        try {
            // 发送回馈消息
            session.sendMessage(new TextMessage("Text message received."));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // 处理客户端发送的二进制消息（视频流数据）
    @Override
    protected void handleBinaryMessage(WebSocketSession session, BinaryMessage message) throws Exception {
        // 处理接收到的二进制消息
        System.out.println("Received binary message of size: " + message.getPayloadLength() + " bytes");

        try {
            // 发送回馈消息
            session.sendMessage(new TextMessage("Binary video data received."));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // 连接关闭时调用
    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        System.out.println("WebSocket connection closed with session id: " + session.getId());
    }

    // 处理连接错误时调用
    @Override
    public void handleTransportError(WebSocketSession session, Throwable exception) throws Exception {
        System.out.println("Error during WebSocket communication: " + exception.getMessage());
    }
}