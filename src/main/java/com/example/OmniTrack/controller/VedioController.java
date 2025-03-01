package com.example.OmniTrack.controller;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
@Controller
public class VedioController {
    @GetMapping("/video")
    public String showVideoPage() {
        return "video";
    }
}
