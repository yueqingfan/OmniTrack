package com.example.OmniTrack.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        // 配置允许的跨域请求路径
        registry.addMapping("/api/users/register")
                .allowedOrigins("http://localhost:8081") // 允许前端的地址
                .allowedMethods("POST") // 允许的请求方式
                .allowedHeaders("*") // 允许所有请求头
                .allowCredentials(true); // 允许发送凭证
    }
}
