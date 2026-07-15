# NetworkAutomationLearning
Python  Refresher and Learning for Network Automation.
## Table of Content
* Review python syntax => Acknowledgement "Traversy Media Python Crash Course 
* learn network automation packages 
* Try automation on GNS-3  
* Python for Network Engineer by Kirk Byers 

# Getting Started

0. Foundation "Stuff"
  * Python
  * Linux/bash fundamentals
  * git
  * REST APIs

1. CLI Based Interactions
  * Python + Netmiko - Configuration Based use cases 
  * Genie CLI - Operation based use cases
  * Parmiko - NOT RECOMMENDED - just use Netmiko

2. Network Automation Frameworks/Abstractions
  * Ansible "Domain Specific Language (DSL)" - Configuration Use Cases
  * NAPALM + Python - Configuration Use Cases
  * Nornir + Python - Configuration Use Cases

3. Network Verification
  * pyATS/Genie + Python - Operational / Testing Use Cases
    * For every BGP neighbor, ensure prefixes being learned
    * For every "up interface", ensure no CRC errors
    * "Profile" before change, Change, "Profile" after, DIFF

Other Skills/Questions
1. How to schedule tasks
  * Run a Python script every hour - cron utility on Linux/Unix/macOS
  * Orchestration/Integration Tools - (CICD Tools) - Jenkins, Drone, Gitlab
    * "Event Driven"
  * Central Management Servers - Ansible Tower


# Real World Use Cases
* Scale
* Performance
* Transactions/Error Recovery

# Ansible File Structure, agentless, modules and API leverage 

# EVE-NG 
* Automated topology creation: dynamically create EVE-NG labs with any number of nodes 
* Configuration deployment: script to apply configuration files to each node efficiently.

# git scrub, remove the commit for deleted files 

  ```bash
  install git-repo-filter 
  
  # find the files removed 
  git show --name-status 

  # run the command , --force if needed 
  git filter-repo \
  --path "path/to/sensitive_file1.py" \
  --path "path/to/sensitive_file2.sh" \
  --invert-paths 

  # add origin back
  git remote add origin <repo>

  # push, -f if required 
  git push -u origin main
  ```