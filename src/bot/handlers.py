from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
import httpx

from aiogram.fsm.context import FSMContext

from src.parsers.telegram import get_participants, load_json, parse_messages
from src.bot.utils import is_subscribed
from src.bot.states import UploadStates
from src.config import CHANNEL_ID
from src.models.schemas import PersonCreate, UserMessage

router = Router()


async def ask_for_file(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UploadStates.waiting_for_file)
    await callback.message.answer("Отправь JSON файл экспорта переписки из Telegram.")
    await callback.answer()

    
@router.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📂 Загрузить переписку", callback_data="upload")]
    ])
    
    await message.answer("""
        <b>Привет! Я StyleMirror 🪞</b>\n\n<i>Я умею отвечать в стиле конкретного человека.\n\nПросто напиши мне любое сообщение — и я отвечу так, как ответил бы он. </i>""", 
        reply_markup=keyboard)


@router.callback_query(F.data == "upload")
async def handle_upload_button(callback: CallbackQuery, state: FSMContext):

    if not await is_subscribed(callback.bot, callback.from_user.id):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Подписаться", url=f"https://t.me/{CHANNEL_ID[1:]}")],
            [InlineKeyboardButton(text="✅ Я подписался", callback_data="confirm_subscription")]
        ])
        await callback.message.edit_text(
            "Для использования бота подпишись на канал 👇",
            reply_markup=keyboard
        )
        await callback.answer()
        return

    await ask_for_file(callback, state)


@router.callback_query(F.data == "confirm_subscription")
async def handle_subscription_confirmation(callback: CallbackQuery, state: FSMContext):
    if not await is_subscribed(callback.bot, callback.from_user.id):
        await callback.answer("❌ Сначала подпишись на канал!", show_alert=True)
        return

    await ask_for_file(callback, state)


@router.message(UploadStates.waiting_for_file, F.document)
async def handle_file(message: Message, state: FSMContext):
    file = await message.bot.get_file(message.document.file_id)
    file_bytes = await message.bot.download_file(file.file_path)
    data = load_json(file_bytes.read())

    participants = get_participants(data)
    if not participants:
        await message.answer("Не удалось найти участников в файле. \n\nПопробуйте ещё раз.")
        return
    
    await state.update_data(json_data=data, participants=participants)
    await state.set_state(UploadStates.waiting_for_person)


    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=p["name"], callback_data=f"person:{p['from_id']}")]
        for p in participants
    ])
    await message.answer("Выбери человека чей стиль копировать:", reply_markup=keyboard)


@router.callback_query(UploadStates.waiting_for_person, F.data.startswith("person:"))
async def handle_person_choice(callback: CallbackQuery, state: FSMContext, http_client: httpx.AsyncClient):
    from_id = callback.data.split(":")[1]
    state_data = await state.get_data()

    person = next(p for p in state_data["participants"] if p["from_id"] == from_id)
    messages = parse_messages(state_data["json_data"], from_id)

    payload = PersonCreate(
        user_id=callback.from_user.id,
        username=callback.from_user.username,
        first_name=callback.from_user.first_name,
        name=person["name"],
        from_id=from_id,
        messages=messages
    )
    await http_client.post("/persons", json=payload.model_dump())

    await callback.message.answer(
        f"Готово! Теперь я буду отвечать в стиле <b>{person['name']}</b>.\n"
        f"Загружено {len(messages)} сообщений.",
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(F.text)
async def handle_text(message: Message, http_client: httpx.AsyncClient):
    payload = UserMessage(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        message_text=message.text
    )
    try:
        response = await http_client.post("/chat", json=payload.model_dump())
        response.raise_for_status()
        data = response.json()
        await message.answer(data["response"])
    except Exception:
        await message.answer("Что-то пошло не так, попробуй позже.")
