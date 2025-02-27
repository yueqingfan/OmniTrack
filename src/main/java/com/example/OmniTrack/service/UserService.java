package com.example.OmniTrack.service;

import com.example.OmniTrack.model.User;
import com.example.OmniTrack.model.LoginRequest;
import com.example.OmniTrack.model.UserRegistrationRequest;
import com.example.OmniTrack.repository.UserRepository;
import org.springframework.stereotype.Service;

@Service
public class UserService {

    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public String register(UserRegistrationRequest userRequest) {
        User user = new User();
        user.setUsername(userRequest.getUsername());
        user.setPassword(userRequest.getPassword());
        user.setEmail(userRequest.getEmail());
        userRepository.save(user);
        return "注册成功";
    }

    public User login(LoginRequest loginRequest) {
        // 这里可以验证用户的用户名和密码，假设验证通过返回一个User对象
        return new User(loginRequest.getUsername(), loginRequest.getPassword(),loginRequest.getEmail());
    }

    public void logout() {
        // 这里可以处理退出的逻辑，例如清除会话
    }
}
