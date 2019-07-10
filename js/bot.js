// Imports
const dotenv = require('dotenv');
const Telegraf = require('telegraf');
dotenv.config();


const bot = new Telegraf(process.env.TOKEN);
bot.start(ctx => ctx.reply('Welcome!'));
bot.help(ctx => ctx.reply('Send me a sticker'));
bot.on('sticker', ctx => ctx.reply('👍'));
bot.hears('hi', ctx => ctx.reply('Hey there'));
bot.command('ping', ({ reply }) => reply('pong'));


const handleStats = async (ctx) => {
  ctx.reply("Here are some stats:")
  console.log(ctx)
  const chat = await ctx.getChat();
  console.log(chat)
}
bot.command('stats', handleStats)

bot.launch();
