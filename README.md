# Cornershop's Backend Test

This technical test requires the design and implementation (using Django) of a management system to coordinate the meal delivery for Cornershop employees.

## Before you begin

You will need to create a private GitHub repository using the information that we provided in this README and invite as collaborators: @Javiergm94 @Stichy23 @Alecornershop.

Should you have any technical questions, please contact osvaldo@cornershopapp.com
Tittle of the project: Backend-Test-(Last Name)

## Description

The current process consist of a person (Nora) sending a text message via Whatsapp to all the chilean employees, the message contains today's menu with the different alternatives for lunch.

> Hello!  
> I share with you today's menu :)
>
> Option 1: Corn pie, Salad and Dessert  
> Option 2: Chicken Nugget Rice, Salad and Dessert  
> Option 3: Rice with hamburger, Salad and Dessert  
> Option 4: Premium chicken Salad and Dessert.
>
> Have a nice day!

With the new system, Nora should be able to:

- Create a menu for a specific date.
- Send a Slack reminder with today's menu to all chilean employees (this process needs to be asynchronous).

The employees should be able to:

- Choose their preferred meal (until 11 AM CLT).
- Specify customizations (e.g. no tomatoes in the salad).

Nora should be the only user to be able to see what the Cornershop employees have requested, and to create and edit today's menu. The employees should be able to specify what they want for lunch but they shouldn't be able to see what others have requested.

NOTE: The slack reminders must contain an URL to today's menu with the following pattern https://nora.cornershop.io/menu/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx (an UUID), this page must not require authentication of any kind.

## Aspects to be evaluated

Since the system is very simple (yet powerful in terms of yumminess) we'll be evaluating, these aspects:

- Functionality
- Testing
- Documentation
- Software design
- Programming style
- Appropriate framework use

## Aspects to be ignored

- Visual design of the solution
- Deployment of the solution

## Restrictions

- The usage of Django's admin is forbidden.
