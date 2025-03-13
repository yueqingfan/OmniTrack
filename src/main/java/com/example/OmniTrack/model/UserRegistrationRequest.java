package com.example.OmniTrack.model;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

public class UserRegistrationRequest {
    @NotBlank(message = "用户名不能为空")
    @Size(min=3,max=20,message = "用户名长度必须在3到20个字符之间")
    private String username;
    @NotBlank(message = "密码不能为空")
    @Size(min=6,message = "密码长度至少六个字符")
    @Pattern(
            regexp = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\\\d)(?=.*[@$!%*?&])[A-Za-z\\\\d@$!%*?&]{6,}$",
            message = "密码必须包含至少一个大写字母、一个小写字母、一个数字和一个特殊字符"
    )
    private String password;
    @NotBlank(message = "邮箱不能为空")
    @Email(message = "邮箱格式不正确")
    private String email;
    public UserRegistrationRequest() {}
    public UserRegistrationRequest(String username, String password, String email) {
        this.username = username;
        this.password = password;
        this.email = email;
    }
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
    @Override
    public String toString() {
        return "UserRegistrationRequest{" +
                "username='" + username + '\'' +
                ", password='" + password + '\'' +
                ", email='" + email + '\'' +
                '}';
    }
}
