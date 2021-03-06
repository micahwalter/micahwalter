---
title: Yubisneezes
description: Hachoo!.
createdAt: 2021-07-02
updatedAt: 2021-07-02
---

There is something that I have discovered called a "Yubisneeze." Let me explain.  
  
A "[Yubikey](https://www.yubico.com/)" is a small device that plugs into your USB port and enables a hardware version of [multi-factor authentication](/multi-factor-authentication) that is very secure and used by businesses large and small. Think of it like a password on top of your password. Most secure sites use MFA devices these days, but most have gone the way of using something like an SMS code texted to the user after they've logged in as a second step, or a virtual MFA device like Google Authenticator which displays a rotating code.  
  
For that extra feeling of protection, hardware devices are the way to go and Yubico makes them. But here's the thing--when you tap your little Yubikey, which is always on and plugged into your laptop, it sends a long string of characters followed by a carriage return. This is meant to make the user experience a tiny bit better by essentially hitting the submit button for you. But, what happens all the time is, you hit the Yubikey by accident while typing in to Slack or some other chat program and you wind up sending the whole channel a "Yubisneeze."  
  
To protect yourself from this ever happening there is a little app called [Yubiswitch](https://github.com/pallotron/yubiswitch), which is smartly designed to give you a little more control over how you interact with the device. Essentially it turns the Yubikey off until you need it, and then once you are done using it, it switches it back off again.  
  
I don't know... this all seems like a really bad UX. Why doesn't Yubico just remove the carriage return and let us live our lives?
