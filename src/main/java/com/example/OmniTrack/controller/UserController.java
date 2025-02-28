package com.example.OmniTrack.controller;

import com.example.OmniTrack.model.User;
import com.example.OmniTrack.model.LoginRequest;
import com.example.OmniTrack.model.UserRegistrationRequest;
import com.example.OmniTrack.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import jakarta.servlet.http.HttpSession;

@RestController
@RequestMapping("/api/users")
public class UserController {

    @Autowired
    private UserService userService;
    @PostMapping("/register")
    public ResponseEntity<String> register(@RequestBody UserRegistrationRequest userRequest) {
        try {
            String result = userService.register(userRequest);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            return ResponseEntity.status(400).body("注册失败: " + e.getMessage());
        }
    }
    @PostMapping("/login")
    public ResponseEntity<String> login(@RequestBody LoginRequest loginRequest, HttpSession session) {
        try {
            User user = userService.login(loginRequest);
            // 用户登录成功，将用户信息存储到 session 中
            session.setAttribute("user", user);
            return ResponseEntity.ok("登录成功");
        } catch (Exception e) {
            return ResponseEntity.status(401).body("登录失败: " + e.getMessage());
        }
    }

    // 退出方法
    @PostMapping("/logout")
    public ResponseEntity<String> logout(HttpSession session) {
        try {
            // 用户登出时，销毁 session
            session.invalidate();
            return ResponseEntity.ok("退出成功");
        } catch (Exception e) {
            return ResponseEntity.status(500).body("退出失败: " + e.getMessage());
        }
    }

    // 判断用户是否登录
    @GetMapping("/checkLogin")
    public ResponseEntity<String> checkLogin(HttpSession session) {
        // 检查 session 中是否存在用户
        if (session.getAttribute("user") != null) {
            return ResponseEntity.ok("已登录");
        } else {
            return ResponseEntity.status(401).body("未登录");
        }
    }

    // 欢迎主页
    @GetMapping("/home")
    public ResponseEntity<String> home() {
        return ResponseEntity.ok("欢迎来到主页！");
    }
}
