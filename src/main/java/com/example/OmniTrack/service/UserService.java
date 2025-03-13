package com.example.OmniTrack.service;

import com.example.OmniTrack.model.User;
import com.example.OmniTrack.model.LoginRequest;
import com.example.OmniTrack.model.UserRegistrationRequest;
import com.example.OmniTrack.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    public String register(UserRegistrationRequest userRequest) {
        if (userRepository.findByUsername(userRequest.getUsername()) != null) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "用户名已存在");
        }
        User user = new User(
                userRequest.getUsername(),
                passwordEncoder.encode(userRequest.getPassword()),
                userRequest.getEmail()
        );

        userRepository.save(user);
        return "注册成功";
    }

    public User login(LoginRequest loginRequest) {
        User user = userRepository.findByUsername(loginRequest.getUsername());
        if (user == null || !passwordEncoder.matches(loginRequest.getPassword(), user.getPassword())) {
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "用户名或密码错误");
        }

        return user;
    }
}