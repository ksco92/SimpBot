# SimpBot

This is a personal project that started as a joke. The idea was to create a bot with fun commands for me and my friends in our DIscord server. I ended up adding more complex stuff based on my friend's requests.

## AWS Set Up

![inf](SimpBot.png)

* Created RDS instance: This keeps track of useless stuff we do.
* Created elasticBeanstalk environment: This is where the bot runs. Created environment inside a new VPC.
* Created IAM role for EB:
  * This needs SecretsManager read permissions.
* Created secret for RDS creds with automatic rotation, because, security.
* Created discord bot following [this](https://discordpy.readthedocs.io/en/latest/discord.html).
* Created secret with bot token.
* Added security group to DB to accept connections from my computer and from the instance in EB.
* Added security group to EB to be able to SSH.

## Database Set Up

* Run the create statements in the database directory.
* Insert discord user ids and nickanmes to the user table.