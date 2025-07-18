#!/bin/bash

{
  echo "User1: Hello everyone!"
  sleep 1
  echo "User2: This sucks"
  sleep 1
  echo "User3: How do I use this?"
  sleep 1
  echo "User4: You are such a noob"
  sleep 1
  echo "User5: Goodbye!"
  sleep 1
  echo "User6: I hate this"
  sleep 1
  echo "User7: LOL, this is terrible"
  sleep 1
  echo "User8: Great job!"
  sleep 1
  echo "User9: You idiot"
  sleep 1
  echo "User10: Nice work!"
} | nc localhost 9999
