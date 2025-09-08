#!/bin/bash

echo "🚀 Replit Selenium 환경 설정 중..."

# Google Chrome 설치
echo "📦 Chrome 설치 중..."
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt-get update
sudo apt-get install -y google-chrome-stable

# ChromeDriver 설치
echo "🔧 ChromeDriver 설치 중..."
sudo apt-get install -y chromium-chromedriver

# 가상 디스플레이 설정
echo "📺 가상 디스플레이 설정 중..."
sudo apt-get install -y xvfb

echo "✅ 설정 완료! 이제 Selenium을 사용할 수 있습니다."