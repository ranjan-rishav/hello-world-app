# Overview
Cloudformation Templates
---
## Contents
* Common infrastructure under **common/** directory
    1. natgw_rtb.yaml: Creates NAT Gateway and corresponding route table
    2. subnets.yaml: Creates 2 Private Subnets
* App infrastructure under **app/** directory
    1. app_alb.yaml: Creates Application Loadbalancer, Target Group, Security Group and Listener
    2. asg_with_dep.yaml: Creates Autoscaling Group, Launch Configuration and Security Group
---
