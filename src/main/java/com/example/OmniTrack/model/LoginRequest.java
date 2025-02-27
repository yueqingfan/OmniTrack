package com.example.OmniTrack.model;

public class LoginRequest {
    private String username;
    private String password;
    private String email;
    // 默认构造函数
    public LoginRequest() {}

    // 带参数的构造函数
    public LoginRequest(String username, String password,String email) {
        this.username = username;
        this.password = password;
        this.email = email;
    }

    // Getter 和 Setter 方法
    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
    public String getEmail() {
        return email;
    }
    public void setEmail(String email) {
        this.email = email;
    }
    // toString 方法，方便调试时查看对象的内容
    @Override
    public String toString() {
        return "LoginRequest{" +
                "username='" + username + '\'' +
                ", password='" + password + '\'' +
                ", email='" + email + '\'' +
                '}';
    }
}
