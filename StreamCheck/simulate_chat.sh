#!/bin/bash
{
  sleep 1; echo "User1: Hello there"
  sleep 1; echo "User2: You suck"
  sleep 1; echo "User3: Damn, this is lame"
  sleep 1; echo "User4: How are you?"
  sleep 1; echo "User5: What the crap is this?"
} | nc localhost 9999
