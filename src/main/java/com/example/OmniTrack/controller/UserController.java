package com.example.OmniTrack.controller;

import com.example.OmniTrack.model.User;
import com.example.OmniTrack.model.LoginRequest;
import com.example.OmniTrack.model.UserRegistrationRequest;
import com.example.OmniTrack.service.UserService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import jakarta.servlet.http.HttpSession;

import java.util.Map;

@RestController
@RequestMapping("/api/users")
public class UserController {

    @Autowired
    private UserService userService;

    @PostMapping("/register")
    public ResponseEntity<?> register(@Valid @RequestBody UserRegistrationRequest userRequest) {
        try {
            String result = userService.register(userRequest);
            return ResponseEntity.ok().body(Map.of("message", result));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("message", "注册失败: " + e.getMessage()));
        }
    }
    @PostMapping("/login")
    public ResponseEntity<?> login(@Valid @RequestBody LoginRequest loginRequest, HttpSession session) {
        try {
            User user = userService.login(loginRequest);
            session.setAttribute("user", user);
            return ResponseEntity.ok().body(Map.of("message", "登录成功"));
        } catch (Exception e) {
            return ResponseEntity.status(401).body(Map.of("message", "登录失败: " + e.getMessage()));
        }
    }
}