# DSA Solver

This repository contains a Data Structures and Algorithms (DSA) learning assistant built using LangChain and LangGraph.

## Overview

The main component is `notebook/clean.ipynb`, which implements an intelligent DSA mentor that uses the Socratic method to guide students through problem-solving.

## Features

### Core Components

- **AI-Powered Mentor**: Uses Google's Gemini 2.5 Flash model for intelligent responses
- **Interactive Learning**: Employs Socratic method - guides through questions rather than giving direct solutions
- **Persistent Python Environment**: Maintains state across code executions for testing solutions

### Available Tools

1. **Python REPL**: Execute and test code solutions
2. **Hint Generator**: Provides subtle hints for DSA problems without revealing solutions
3. **Test Case Generator**: Creates test cases for problem validation
4. **Bug Hint Tool**: Analyzes code for logic issues and provides debugging hints
5. **Complexity Analyzer**: Evaluates time and space complexity of solutions
6. **Code Quality Checker**: Reviews code for style, readability, and best practices
7. **Problem Recommender**: Suggests next problems based on current progress
8. **Study Plan Creator**: Generates personalized DSA study plans

### Learning Methodology

The system follows a structured approach:
1. Problem understanding through clarifying questions
2. Automatic test case generation
3. Guided solution development
4. Code testing and validation
5. Debugging assistance when needed
6. Complexity analysis of working solutions
7. Code quality review and improvements
8. Progress-based problem recommendations

## Setup

1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   - `GOOGLE_API_KEY`: Your Google AI API key
   - `LANGSMITH_API_KEY`: Your LangSmith API key (for tracing)

3. Run the notebook to start the interactive DSA mentor

## Usage

The system automatically:
- Generates hints and test cases when you share a problem
- Analyzes code for bugs when you share solutions
- Provides complexity analysis for working code
- Recommends next problems based on your progress

Simply interact with the mentor by describing DSA problems or sharing code for review.

## Key Benefits

- **No Direct Solutions**: Promotes deep learning through guided discovery
- **Proactive Assistance**: Tools are used automatically based on context
- **Comprehensive Analysis**: Covers correctness, complexity, and code quality
- **Personalized Learning**: Adapts recommendations to individual progress
