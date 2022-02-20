
DIRECT_FILE_LINK_URL: str = 'https://files.slack.com'


class AD_VIEW_INDENTS:
    DESCRIPTION : str = "*Description*" # bold
    PRICE       : str = "Price"
    CONDITION   : str = "*Condition*" # bold


class POST_MESSAGES:
    NEW_AD_ADDED        : str = "New advertisment post is added"
    PRICE_CHANGED       : str = "Price is changed"
    HOME_APP            : str = "App window open"
    ITEM_SOLD           : str = "Item is marked as sold"
    ITEM_PHOTO_SHARED   : str = "Item photo is shared"


class BUTTON_ACTION_IDS:
    CHANGE_PRICE            : str = "change_price_btn"
    CREATE_ADVERTISMENT     : str = "create_advertisment_btn"
    DELETE_PREVIEW_IMAGE    : str = "delete_preview_image_btn"
    BUY_ITEM                : str = "buy_item_btn"
    MARK_SOLD               : str = "mark_as_sold_btn"
    SHOW_MORE_ITEM_PHOTOS   : str = "more_item_photos_btn"


class INPUT_ACTION_IDS:

    # view to describe an item specification
    POST_TOPIC              : str = "post_topic_action_id"
    PREVIEW_ITEM_IMAGE_URL  : str = "preview_item_image_url_action_id"
    MORE_ITEM_IMAGES_URL    : str = "more_item_images_url_action_id"
    ITEM_PRICE              : str = "item_price_action_id"
    ITEM_CONDITION          : str = "item_condition_action_id"
    ITEM_DESCRIPTION        : str = "item_description_action_id"


class VIEW_IDS:
    ITEM_SPECIFICATION   : str = "stuff_specification_view"
    INPUT_NEW_ITEM_PRICE : str = "new_item_price_view"


class BLOCK_IDS:

    # sale post in the channel (*ad - advertisment):
    AD_TOPIC                : str = "ad_topic_block_id"
    AD_ITEM_DESCRIPTION     : str = "ad_item_description_block_id"
    AD_ITEM_PRICE           : str = "ad_item_price_block_id"
    AD_ITEM_CONDITION       : str = "ad_item_conditions_block_id"
    AD_ITEM_PREVIEW_IMAGE   : str = "ad_item_preview_image_block_id"
    AD_SALE_CONDITION       : str = "ad_sale_condition_block_id"
    AD_ADMIN_ACTION_BUTTONS : str = "ad_admin_action_buttons_block_id"
    AD_USER_ACTION_BUTTONS  : str = "ad_user_action_buttons_block_id"
    
    # view to change an item price
    INPUT_NEW_ITEM_PRICE    : str = "input_new_item_price_block_id"
    MESSAGE_TS_CONTEXT      : str = "message_ts_block_id" # this block is used to transfer message timestamp to change and delete post with an old price
    CHANNEL_ID_CONTEXT      : str = "channel_id_block_id" # this block is used to transfer message timestamp to change and delete post with an old price

    # view to describe an item specification
    INPUT_ITEM_DESCRIPTION       : str = "input_item_description_block_id"
    SELECT_ITEM_CONDITION        : str = "select_item_condition_block_id"
    INPUT_ITEM_PRICE             : str = "input_item_price_block_id"
    INPUT_MORE_ITEM_IMAGES_URL   : str = "input_more_item_images_url_block_id"
    INPUT_PREVIEW_ITEM_IMAGE_URL : str = "input_preview_item_image_url_block_id"
    INPUT_POST_TOPIC             : str = "input_post_topic_block_id"


class EVENTS_IDS:
    APP_HOME_OPENED: str = "app_home_opened"
    FILE_SHARED: str = "file_shared"


class COMMANDS_IDS:
    POST: str = "/post"