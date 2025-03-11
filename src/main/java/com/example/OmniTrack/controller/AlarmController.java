package com.example.OmniTrack.controller;

import com.example.OmniTrack.model.AlarmRecord;
import com.example.OmniTrack.repository.AlarmRecordsRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.time.LocalDateTime;
import java.util.List;

@Slf4j
@RestController
@RequestMapping("/api/alarms")
@CrossOrigin(origins = "http://localhost:8081")
public class AlarmController {

    @Autowired
    private AlarmRecordsRepository alarmRecordsRepository;

    @GetMapping
    public List<AlarmRecord> getAllAlarms() {
        return alarmRecordsRepository.findAll(Sort.by(Sort.Direction.DESC, "timestamp"));
    }

    @PostMapping
    public ResponseEntity<String> saveAlarm(@RequestBody AlarmRecord alarmRecord) {
        log.info("收到报警请求: label={}, confidence={}, imageUrl.length={}",
                alarmRecord.getLabel(),
                alarmRecord.getConfidence(),
                alarmRecord.getImageUrl() != null ? alarmRecord.getImageUrl().length() : 0);

        // 检查数据是否完整
        if (alarmRecord.getLabel() == null || alarmRecord.getImageUrl() == null) {
            return ResponseEntity.badRequest().body("数据不完整");
        }

        // 如果时间戳未设置，则设置为当前时间
        if (alarmRecord.getTimestamp() == null) {
            alarmRecord.setTimestamp(LocalDateTime.now());
        }

        try {
            alarmRecordsRepository.save(alarmRecord);
            log.info("报警记录已存入数据库");
            return ResponseEntity.ok("报警记录已保存");
        } catch (Exception e) {
            log.error("保存报警记录失败", e);
            return ResponseEntity.status(500).body("保存报警记录失败");
        }
    }
}
