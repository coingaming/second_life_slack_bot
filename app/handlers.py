
import asyncio
from typing import NoReturn, List, Dict, Optional
from functools import partial
from .async_app import SecondlifeBotApp
from .utils import create_image_direct_url, get_file_id
from .settings import APP_SLACK_TOKEN
from .ui import get_item_ad_blocks, get_stuff_specification_view, get_ad_confirmation_blocks, get_message_blocks, \
	change_item_price_view
from .constants import AD_VIEW_INDENTS, POST_MESSAGES, BUTTON_ACTION_IDS, VIEW_IDS, \
	EVENTS_IDS, COMMANDS_IDS, BLOCK_IDS, INPUT_ACTION_IDS


def setup_requests_handlers(app: SecondlifeBotApp, config: Dict) -> NoReturn:
	# events: 
	# - app_home_opened
	# - file_shared
	events_handlers(app, config)
	# commands:
	# - /post
	commands_handlers(app, config)
	# actions:
	# - change price
	# - create advertisment
	# - delete item im age preview
	# - buy an item
	# - mark item as sold
	# - show more item photos
	action_handlers(app, config)
	# views:
	# - new item price
	# - item specification
	view_handlers(app, config)


def view_handlers(app: SecondlifeBotApp, config: Dict) -> NoReturn:


	@app.view(VIEW_IDS.INPUT_NEW_ITEM_PRICE)
	async def on_new_price_view_id(ack, body, client, logger):

		"""
			View to provide new price for the posted advertisment
		"""
		await ack()
		logger.info(f"User: {body['user']['id']} invoked view: {VIEW_IDS.INPUT_NEW_ITEM_PRICE}")

		state_values: Dict = body['view']['state']['values']
		for value in state_values.items():
			match value:
				case (
					BLOCK_IDS.INPUT_NEW_ITEM_PRICE, 
					{
						'plain_text_input-action': {
							'type': 'plain_text_input', 
							'value': new_price
						}
					}):
					new_price: str = new_price
					break
		blocks: List = body['view']['blocks']
		for block in blocks:
			match block:
				case {
					'block_id': BLOCK_IDS.MESSAGE_TS_CONTEXT, 
					'elements': [{'text': value}]
					}:
					message_ts: str = value
				case {
					'block_id': BLOCK_IDS.CHANNEL_ID_CONTEXT, 
					'elements': [{'text': value}]
					}:
					channel_id: str = value
		messages_history: Dict = await client.conversations_history(
			channel=channel_id,
			inclusive=True,
			latest = message_ts,
        	limit = 1 # looking only for a message with specified timestamp (message_ts)
		)

		for message in messages_history['messages']:
			match message:
				case {'ts': message_ts}:
					old_message_blocks: Dict = message['blocks']
					break

		replies_info: Dict = await client.conversations_replies(
			channel=channel_id,
        	ts=message_ts,
		)

		# delete message and all replies
		replies: List = replies_info['messages']
		await asyncio.gather(
			*[
				client.chat_delete(
					channel=channel_id, 
					ts=reply['ts']
				) for reply in replies
			]
		)

		# parse previos message block
		more_images_url: Optional[str] = None
		preview_image_url: Optional[str] = None
		for block in old_message_blocks:
			match block:
				case {
					'block_id': BLOCK_IDS.AD_TOPIC, 
					'text': {
						'text': value
						}
					}:
					topic: str = value
				case {
					'block_id': BLOCK_IDS.AD_ITEM_PREVIEW_IMAGE, 
					'image_url': value
					}:
					preview_image_url: Optional[str] = value
				case {
					'block_id': BLOCK_IDS.AD_ITEM_DESCRIPTION, 
					'text': {
						'text': value
						}
					}:
					description: str = value.replace(f"{AD_VIEW_INDENTS.DESCRIPTION}\n", "")
				case {
					'block_id': BLOCK_IDS.AD_ITEM_CONDITION, 
					'text': {
						'text': value
						}
					}:
					item_condition: str = value.replace(f"{AD_VIEW_INDENTS.CONDITION}\n", "")
				case {
					'block_id': BLOCK_IDS.AD_USER_ACTION_BUTTONS, 
					'elements': user_action_elements
					}:

					for action_element in user_action_elements:
						match action_element:
							case {
								'action_id': BUTTON_ACTION_IDS.SHOW_MORE_ITEM_PHOTOS, 
								'url': value
								}:
								more_images_url: Optional[str] = value
								break
		# post new message
		await client.chat_postMessage(
			channel=channel_id,
			text=POST_MESSAGES.PRICE_CHANGED,
			blocks=get_item_ad_blocks(
				topic, 
    			preview_image_url, 
				more_images_url,
    			description,
    			new_price, 
    			item_condition
			)
		)


	@app.view(VIEW_IDS.ITEM_SPECIFICATION)
	async def on_stuff_specification_view(ack, body, client, logger):

		"""
			Stuff specification view contains field describing at item (image, price e.t.c.)
		"""

		await ack()
		logger.info(f"User: {body['user']['id']} invoked view: {VIEW_IDS.ITEM_SPECIFICATION}")

		blocks_values: Dict = body['view']['state']['values']
		for _, action_info in blocks_values.items():

			match action_info:
				case {
					INPUT_ACTION_IDS.POST_TOPIC: 
						{
							"type": type, 
							"value": value
						}
					}:
					topic: str = f"{value}"
				case {
					INPUT_ACTION_IDS.PREVIEW_ITEM_IMAGE_URL: 
						{
							'type': type, 
							'value': value
						}
					}:
					image_url: Optional[str] = value
				case {
					INPUT_ACTION_IDS.MORE_ITEM_IMAGES_URL: {
						'type': type, 
						'value': value
						}
					}:
					more_images_url: Optional[str] = value
				case {
					INPUT_ACTION_IDS.ITEM_PRICE: {
						'type': type, 
						'value': value
						}
					}:
					price: str = value
				case {
					INPUT_ACTION_IDS.ITEM_DESCRIPTION: {
						'type': type, 
						'value': value
						}
					}:
					description: str = value
				case {
					INPUT_ACTION_IDS.ITEM_CONDITION: {
						'type': type, 
						'selected_option': {'value': value}
						}
					}:
					item_condition: str = value
		await client.chat_postMessage(
			channel=config["channel_to_post_advertisments"],
			text=POST_MESSAGES.NEW_AD_ADDED,
			blocks=get_item_ad_blocks(
				topic, 
    			image_url, 
				more_images_url,
    			description, 
    			price, 
    			item_condition
			)
		)


def action_handlers(app: SecondlifeBotApp, config: Dict=None) -> NoReturn:


	@app.action(BUTTON_ACTION_IDS.CHANGE_PRICE)
	async def on_change_price_btn(ack, body, client, logger):

		"""
			Pushing this button admin can change item price. 
			After changing price the old ad will be deleted
		"""

		await ack()
		logger.info(f"User: {body['user']['id']} pushed button: {BUTTON_ACTION_IDS.CHANGE_PRICE}")

		trigger_id: str = body["trigger_id"]
		message_ts: str = body['container']['message_ts']
		channel_id: str = body['container']['channel_id']
		slack_user_id: str = body['user']['id']

		if not config["debug"]:
			users_list_info: Dict = await client.usergroups_users_list(
					usergroup=config["user_group"]
			)
			user_id: str = body['user']['id']
			users_list: List = users_list_info["users"]
			if user_id not in users_list:
				return await client.chat_postEphemeral(
          				channel=channel_id,
          				user=slack_user_id,
          				text=f"Only techOps team members can change a price"
      				)
		await client.views_open(
           	trigger_id=trigger_id,
           	view=change_item_price_view(message_ts, channel_id)
      	)


	@app.action(BUTTON_ACTION_IDS.CREATE_ADVERTISMENT)
	async def on_create_ad_btn(ack, body, client, logger):

		"""
			Pushing this button invokes a stuff specification view to fill
		"""

		await ack()
		logger.info(f"User: {body['user']['id']} pushed button: {BUTTON_ACTION_IDS.CREATE_ADVERTISMENT}")

		channel: str = body['channel']['id']
		timestamp: str = body['message']['ts']
		trigger_id: str = body["trigger_id"]
		file_id: str = body['actions'][0]['value'] # todo remove hardcode, get value by action_id

		# todo remove extra API call (call API twice)
		file_info: Dict = await client.files_info(
			token=APP_SLACK_TOKEN,
			file=file_id
		)
		image_direct_url: Optional[str] = create_image_direct_url(file_info)
		specification_view: Dict = get_stuff_specification_view(image_direct_url)
		await client.views_open(
            trigger_id=trigger_id,
            view=specification_view
        )
		await client.chat_delete(
			channel=channel,
			ts=timestamp
		)


	@app.action(BUTTON_ACTION_IDS.DELETE_PREVIEW_IMAGE)
	async def on_delete_stuff_image_btn(ack, body, client, logger):

		"""
			Pushing this button will remove stuff image (if admin user changed his mind)
			which is linked with an advertisment post
		"""

		await ack()
		logger.info(f"User: {body['user']['id']} pushed button: {BUTTON_ACTION_IDS.DELETE_PREVIEW_IMAGE}")

		channel_id: str = body['channel']['id']
		timestamp: str = body['message']['ts']
		file_id: str = body['actions'][0]['value'] # todo remove hardcode, get value by action_id
		await client.chat_delete(
			channel=channel_id,
			ts=timestamp
		)
		await client.files_delete(
			token=APP_SLACK_TOKEN,
			file=file_id,
		)


	@app.action(BUTTON_ACTION_IDS.BUY_ITEM)
	async def on_want_buy_btn(ack, body, client, logger):

		"""
			User wanted to buy an item
			After pushing the button app will put his name into replies
		"""

		await ack()
		logger.info(f"User: {body['user']['id']} pushed button: {BUTTON_ACTION_IDS.BUY_ITEM}")

		timestamp: str = body['container']['message_ts']
		channel_id: str = body['container']['channel_id']
		user_id: str = body['user']['id']
		replies_info: Dict = await client.conversations_replies(
			channel=channel_id,
        	ts=timestamp,
		)
		replies_messages: List = replies_info['messages']
		replies_num: int = len(replies_messages)
		reply_text: str = f"<@{user_id}> wants to buy it. "
		match replies_num:
			case 1:
				reply_text += "Congrats, you're :one:"

		await client.chat_postMessage(
			channel=channel_id,
			text=reply_text,
			thread_ts=timestamp
		)


	@app.action(BUTTON_ACTION_IDS.MARK_SOLD)
	async def on_mark_as_sold_btn(ack, body, client, logger):

		"""
			Admin user marked an item as sold
		"""

		await ack()
		logger.info(f"User: {body['user']['id']} pushed button: {BUTTON_ACTION_IDS.MARK_SOLD}")

		channel_id: str = body['container']['channel_id']
		slack_user_id: str = body['user']['id']
		if not config["debug"]:
			users_list_info: Dict = await client.usergroups_users_list(
					usergroup=config["user_group"]
			)
			user_id: str = body['user']['id']
			users_list: List = users_list_info["users"]
			if user_id not in users_list:
				return await client.chat_postEphemeral(
	    			channel=channel_id,
	    			user=slack_user_id,
	    			text=f"Only techOps team members can mark an item as sold"
				)

		timestamp: str = body['container']['message_ts']
		blocks: List = body['message']['blocks']
		slack_user_id: str = body['user']['id']
		for block in blocks:
			if block['type'] == 'image':
				is_ad_with_image: bool = True
				image_url: str = block['image_url']
				file_id: str = get_file_id(image_url)
				break
		else:
			is_ad_with_image: bool = False

		topic_block: str
		rest_blocks: List
		if is_ad_with_image:
			# skip these blocks:
			# _1 - admin action buttons
			# _2 - preview image
			# _3 - user action buttons
			topic_block, _1, _2, *rest_blocks, _3 = blocks
			# delete image
			await client.files_delete(
				token=APP_SLACK_TOKEN,
				file=file_id,
			)
		else:
			# skip these blocks:
			# _1 - admin action buttons
			# _2 - user action buttons
			topic_block, _1, *rest_blocks, _2 = blocks
		topic_block['text']['text'] = "Item is sold :checkered_flag:"
		# skipping buttons and image
		blocks_marked_sold: List = [topic_block, *rest_blocks]
		await client.chat_update(
			channel=channel_id,
			text=POST_MESSAGES.ITEM_SOLD,
			ts=timestamp,
			blocks=blocks_marked_sold
		)


	@app.action(BUTTON_ACTION_IDS.SHOW_MORE_ITEM_PHOTOS)
	async def on_show_more_item_photos(ack, body, logger):

		"""
			User wants to see more item photos, redirect him to google drive e.t.c
		"""

		await ack()
		logger.info(f"User: {body['user']['id']} pushed button: {BUTTON_ACTION_IDS.SHOW_MORE_ITEM_PHOTOS}")


def commands_handlers(app: SecondlifeBotApp, config: Dict=None) -> NoReturn:


	@app.command(COMMANDS_IDS.POST)
	async def on_create_post(ack, body, client, logger):

		"""
			User entered '/post' command to specify an item description
		"""

		await ack()
		logger.info(f"User: {body['user_id']} invoked command: {COMMANDS_IDS.POST}")

		await client.views_open(
            trigger_id=body["trigger_id"],
            view=get_stuff_specification_view()
        )


def events_handlers(app: SecondlifeBotApp, config: Dict=None) -> NoReturn:


	@app.event(EVENTS_IDS.APP_HOME_OPENED)
	async def on_app_home_opened(ack, body, client, logger):

		"""
			User opened appplication home tab
			So far we handle only message tab to offer help view
		"""

		await ack()
		tab: str = body['event']['tab']
		if tab != 'messages':
			# app home tab is not proceed for now
			return

		logger.info(f"User: {body['event']['user']} thrown the event: {EVENTS_IDS.APP_HOME_OPENED}")
		channel: str = body['event']['channel']
		response: Dict = await client.chat_postMessage(
			token=APP_SLACK_TOKEN,
			channel=channel,
			text=POST_MESSAGES.HOME_APP,
			blocks=get_message_blocks()
		)

		await asyncio.sleep(config["home_app_view_delay"])
		message_timestamp: str = response['ts']
		await client.chat_delete(
			token=APP_SLACK_TOKEN,
			channel=channel,
			ts=message_timestamp
		)


	@app.event(EVENTS_IDS.FILE_SHARED)
	async def on_file_shared(ack, body, client, logger):

		"""
			User shared file to bound it with an advertisment post
		"""

		await ack()
		logger.info(f"User: {body['event']['user_id']} thrown the event: {EVENTS_IDS.FILE_SHARED}")

		file_id: str = body['event']['file_id']
		channel_id: str = body['event']['channel_id']
		file_info: Dict = await client.files_info(
			token=APP_SLACK_TOKEN,
			file=file_id
		)
		if not file_info['file']['public_url_shared']:
			await client.files_sharedPublicURL(
				token=APP_SLACK_TOKEN,
				file=file_id
			)
		await client.chat_postMessage(
			channel=channel_id,
			text=POST_MESSAGES.ITEM_PHOTO_SHARED,
			blocks=get_ad_confirmation_blocks(file_id)
		)