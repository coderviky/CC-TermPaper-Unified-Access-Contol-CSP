--create admin
INSERT INTO employees (name, username, password, email, role)
VALUES ('Admin Name', 'admin', 'admin', 'admin@email.com', 'ADMIN');


-- create iam user for admin
INSERT INTO iamdetails (role, iam_user, accesskey, permissions)
VALUES ('ADMIN', 'admin_iam_user', 'admin_access_key', '[\"admin_permission_1\", \"admin_permission_2\"]');


-- Associate the IAM details with the admin employee
UPDATE employees
SET iam_id = LAST_INSERT_ID()
WHERE username = 'admin';
-- insert into permissions ("id","role","")


-- create permissions
 INSERT INTO permissions (role, type, permissions)
VALUES ('DEVELOPER', 'object', '[\"PUT_OBJECT\", \"GET_OBJECT\"]'),
       ('DEVELOPER', 'bucket', '[\"PUT_BUCKET\", \"GET_BUCKET\"]'),
       ('AUDITOR', 'object', '[\"GET_OBJECT\"]'),
       ('ADMIN', 'bucket', '[\"PUT_BUCKET\", \"DELETE_BUCKET\"]');


-- create developer bucket
INSERT INTO buckets (bucket_id, bucket_csp, comment, bucket_type)
VALUES ('developer_bucket_id', 'AWS', 'Developer bucket comment', 'DEVELOPER');

