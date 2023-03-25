INSERT INTO public.users (display_name, handle, cognito_user_id)
VALUES
  ('Andrew Brown', 'andrewbrown' ,'MOCK'),
  ('Andrew Bayko', 'bayko' ,'MOCK'),
  ('Shimaa Badawy', 'shimaa', 'MOCK');


INSERT INTO public.activities (uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'andrewbrown' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  ),
  (
    (SELECT uuid from public.users WHERE users.handle = 'shimaa' LIMIT 1 ),
    'Hello World!!!!!',
    current_timestamp + interval '5 day'
  ),
   (
    (SELECT uuid from public.users WHERE users.handle = 'bayko' LIMIT 1 ),
    'Hello World!!!!!',
    current_timestamp + interval '1 day'
  );