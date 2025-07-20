import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from config import BOT_TOKEN, ADMIN_IDS, DB_NAME, PAYMENT_NUMBERS
from db import init_db, add_user, get_user, add_task, get_tasks, submit_proof, get_pending_submissions, approve_submission, get_stats, add_recharge, get_recharges
from utils import is_admin

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    user = get_user(message.from_user.id)
    if user:
        await message.answer("You are already registered.")
    else:
        add_user(message.from_user.id, message.from_user.full_name)
        await message.answer("Welcome! You have been registered with 200 bonus coins.")

@dp.message(F.text == "/tasks")
async def task_list(message: Message):
    tasks = get_tasks()
    if not tasks:
        await message.answer("No tasks available right now.")
        return
    for task in tasks:
        await message.answer(f"📌 <b>{task[1]}</b>
{task[2]}
Slots: {task[4]}/{task[3]}
Send proof: /submit_{task[0]}")

@dp.message(F.text.regexp(r"^/submit_(\d+)$"))
async def submit_task(message: Message):
    task_id = int(message.text.split("_")[1])
    await message.answer(f"Send your proof for task {task_id}:")
    dp.message.register(lambda m: handle_proof(m, task_id), F.content_type.in_({"text", "photo"}))

async def handle_proof(message: Message, task_id: int):
    proof = message.text or message.caption or "proof"
    submit_proof(user_id=message.from_user.id, task_id=task_id, proof=proof)
    await message.answer("Proof submitted. Awaiting admin approval.")

@dp.message(F.text.startswith("/add_task"))
async def add_task_handler(message: Message):
    if not is_admin(message.from_user.id): return
    try:
        _, title, desc, slots = message.text.split("|")
        add_task(title.strip(), desc.strip(), int(slots.strip()))
        await message.answer("✅ Task added.")
    except:
        await message.answer("Use format: /add_task|Title|Description|Slots")

@dp.message(F.text == "/pending")
async def pending_subs(message: Message):
    if not is_admin(message.from_user.id): return
    subs = get_pending_submissions()
    for s in subs:
        await message.answer(f"User: {s[1]}
Task ID: {s[2]}
Proof: {s[3]}
/approve_{s[0]}")

@dp.message(F.text.regexp(r"^/approve_(\d+)$"))
async def approve_sub(message: Message):
    if not is_admin(message.from_user.id): return
    sub_id = int(message.text.split("_")[1])
    approve_submission(sub_id)
    await message.answer("✅ Approved.")

@dp.message(F.text.startswith("/recharge"))
async def recharge_handler(message: Message):
    try:
        _, method, amount = message.text.split("|")
        if method not in PAYMENT_NUMBERS:
            await message.answer("Invalid method.")
            return
        add_recharge(message.from_user.id, method, int(amount))
        await message.answer(f"Send {amount} to {PAYMENT_NUMBERS[method]} and wait for approval.")
    except:
        await message.answer("Use: /recharge|bkash|100")

@dp.message(F.text == "/admin_stats")
async def admin_stats(message: Message):
    if not is_admin(message.from_user.id): return
    u, t, s = get_stats()
    await message.answer(f"Users: {u}
Tasks: {t}
Submissions: {s}")

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())