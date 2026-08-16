-- SQL Schema definition for Smart Internship Management System
-- Compatible with both Snowflake and SQLite

-- 1. Students Table
CREATE TABLE IF NOT EXISTS Students (
    student_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    skills TEXT,
    resume_name VARCHAR(255),
    resume_path VARCHAR(555),
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Companies Table
CREATE TABLE IF NOT EXISTS Companies (
    company_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    website VARCHAR(255),
    location VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Internships Table
CREATE TABLE IF NOT EXISTS Internships (
    internship_id VARCHAR(50) PRIMARY KEY,
    company_id VARCHAR(50) NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(255) NOT NULL,
    requirements TEXT,
    skills_required VARCHAR(255),
    duration VARCHAR(50),
    stipend VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Applications Table
CREATE TABLE IF NOT EXISTS Applications (
    application_id VARCHAR(50) PRIMARY KEY,
    internship_id VARCHAR(50) NOT NULL,
    student_id VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'Applied', -- 'Applied', 'Reviewed', 'Accepted', 'Rejected'
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Admins Table
CREATE TABLE IF NOT EXISTS Admins (
    admin_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. SkillAnalysis Table (Future Expansion)
CREATE TABLE IF NOT EXISTS SkillAnalysis (
    analysis_id VARCHAR(50) PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    skills_gap TEXT,
    recommended_courses TEXT,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. DocumentVerification Table (Future Expansion)
CREATE TABLE IF NOT EXISTS DocumentVerification (
    verification_id VARCHAR(50) PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    document_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending', -- 'Pending', 'Verified', 'Rejected'
    verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
