-- Update num_checkins
UPDATE Business
SET num_checkins = (SELECT SUM(Checkins.count)
FROM Checkins
WHERE Checkins.business_id=Business.business_id
GROUP BY Business.business_id)

UPDATE Business
SET num_checkins = 0
WHERE num_checkins IS NULL

-- Update review_count
UPDATE Business
SET review_count = (SELECT COUNT(Reviews.review_id)
FROM Reviews
WHERE Reviews.business_id=Business.business_id
GROUP BY Business.business_id)

UPDATE Business
SET review_count = 0
WHERE review_count IS NULL

-- Update reviewrating
UPDATE Business
SET reviewrating = (SELECT SUM(Reviews.review_stars)/COUNT(Reviews.review_stars)
FROM Reviews
WHERE Reviews.business_id=Business.business_id
GROUP BY Business.business_id)