-- XBook Database Initialization Script
-- This script runs on first-time PostgreSQL container startup

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text similarity search

-- Create schemas (if needed for multi-tenant later)
-- CREATE SCHEMA IF NOT EXISTS xbook;

-- Set timezone
SET timezone = 'UTC';

-- You can add initial data here if needed
-- For example, default admin user, test data, etc.

COMMENT ON DATABASE xbook IS 'XBook - Language Learning Platform Database';
