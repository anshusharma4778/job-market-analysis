-- ============================================================
-- Job Market Analysis — SQL Queries
-- Run these after loading cleaned data into SQLite/PostgreSQL
-- ============================================================

-- 1. Top 10 In-Demand Job Roles
SELECT job_title, COUNT(*) AS job_count
FROM job_postings
GROUP BY job_title
ORDER BY job_count DESC
LIMIT 10;

-- 2. Job Type Distribution (Remote vs Onsite vs Hybrid)
SELECT job_type, COUNT(*) AS count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM job_postings), 2) AS percentage
FROM job_postings
GROUP BY job_type
ORDER BY count DESC;

-- 3. Job Level Distribution
SELECT job_level, COUNT(*) AS count
FROM job_postings
GROUP BY job_level
ORDER BY count DESC;

-- 4. Top 10 Hiring Companies
SELECT company, COUNT(*) AS openings
FROM job_postings
GROUP BY company
ORDER BY openings DESC
LIMIT 10;

-- 5. Top Locations for Data Jobs
SELECT job_location, COUNT(*) AS job_count
FROM job_postings
GROUP BY job_location
ORDER BY job_count DESC
LIMIT 10;

-- 6. Jobs by Country
SELECT search_country, COUNT(*) AS job_count
FROM job_postings
GROUP BY search_country
ORDER BY job_count DESC;

-- 7. Mid-Senior vs Associate Roles by Company (Top 5)
SELECT company, job_level, COUNT(*) AS count
FROM job_postings
WHERE company IN (
    SELECT company FROM job_postings
    GROUP BY company ORDER BY COUNT(*) DESC LIMIT 5
)
GROUP BY company, job_level
ORDER BY company, count DESC;

-- 8. Jobs Mentioning AI/ML Skills
SELECT COUNT(*) AS ai_jobs,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM job_skills), 2) AS pct_of_total
FROM job_skills
WHERE job_skills LIKE '%Machine Learning%'
   OR job_skills LIKE '%Artificial Intelligence%'
   OR job_skills LIKE '%Deep Learning%'
   OR job_skills LIKE '%LLM%'
   OR job_skills LIKE '%Generative AI%';

-- 9. Top Skills Overall
SELECT skill, COUNT(*) AS demand
FROM (
    SELECT TRIM(value) AS skill
    FROM job_skills,
    json_each('["' || REPLACE(job_skills, ', ', '","') || '"]')
) sub
GROUP BY skill
ORDER BY demand DESC
LIMIT 20;
