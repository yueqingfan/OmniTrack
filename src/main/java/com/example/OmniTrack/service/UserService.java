package com.example.OmniTrack.service;

import com.example.OmniTrack.model.User;
import com.example.OmniTrack.model.LoginRequest;
import com.example.OmniTrack.model.UserRegistrationRequest;
import com.example.OmniTrack.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;
    public String register(UserRegistrationRequest userRequest) {
        if (userRepository.findByUsername(userRequest.getUsername()) != null) {
            throw new RuntimeException("用户名已存在");
        }
        User user = new User(userRequest.getUsername(), userRequest.getPassword(), userRequest.getEmail());
        userRepository.save(user);
        return "注册成功";
    }
    public User login(LoginRequest loginRequest) {
        User user = userRepository.findByUsername(loginRequest.getUsername());
        if (user == null || !user.getPassword().equals(loginRequest.getPassword())) {
            throw new RuntimeException("用户名或密码错误");
        }
        return user;
    }

    public void logout() {
    }
}
