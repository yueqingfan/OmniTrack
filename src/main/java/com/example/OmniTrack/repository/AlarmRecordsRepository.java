package com.example.OmniTrack.repository;

import com.example.OmniTrack.model.AlarmRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AlarmRecordsRepository extends JpaRepository<AlarmRecord,Long> {
}
