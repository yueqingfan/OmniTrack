CREATE DATABASE IF NOT EXISTS omniTrackDB;
USE omniTrackDB;
CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
CREATE UNIQUE INDEX idx_username ON users(username);
CREATE UNIQUE INDEX idx_email ON users(email);
CREATE TABLE alarm_records (
                               id BIGINT AUTO_INCREMENT PRIMARY KEY,
                               label VARCHAR(255),
                               confidence DOUBLE,
                               image_url TEXT,
                               timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
