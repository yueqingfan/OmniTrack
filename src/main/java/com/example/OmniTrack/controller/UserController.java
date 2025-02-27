package com.example.OmniTrack.controller;

import com.example.OmniTrack.model.User;
import com.example.OmniTrack.model.LoginRequest;
import com.example.OmniTrack.model.UserRegistrationRequest;
import com.example.OmniTrack.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
public class UserController {

    @Autowired
    private UserService userService;

    @PostMapping("/register")
    public ResponseEntity<String> register(@RequestBody UserRegistrationRequest userRequest) {
        String result = userService.register(userRequest);
        return ResponseEntity.ok(result);
    }

    @PostMapping("/login")
    public ResponseEntity<User> login(@RequestBody LoginRequest loginRequest) {
        User user = userService.login(loginRequest);
        return ResponseEntity.ok(user);
    }

    @PostMapping("/logout")
    public ResponseEntity<String> logout() {
        userService.logout();
        return ResponseEntity.ok("退出成功");
    }

    @GetMapping("/home")
    public ResponseEntity<String> home() {
        return ResponseEntity.ok("欢迎来到主页！");
    }
}
