from typing import List, Dict, Optional
from ..constants import AD_VIEW_INDENTS, BUTTON_ACTION_IDS, VIEW_IDS, BLOCK_IDS, INPUT_ACTION_IDS


def get_home_tab_view(user_id) -> Dict:
    view: Dict ={
        "type": "home",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Welcome, <@" + user_id + ">*"
                }
            },
            {
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": ":black_small_square: The application allows you to create an ad and post it to the #secondlife channel;"
                }
            },
			{
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": ":black_small_square: Interaction with the application is done through the *Messages tab*;"
                }
            },
			{
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": ":black_small_square: To start creating an ad, you need to either *upload a photo* (it will be displayed in the preview) or enter the */post* command (an ad without a preview);"
                }
            },
			{
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": ":black_small_square: If a user is interested in buying, he can click the *I want to buy* button;"
                }
            },
			{
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": ":black_small_square: After clicking the *I want to buy* button, a thread will be created that will indicate that the user wants to purchase the product;"
                }
            },
			{
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": ":black_small_square: If the author of the post provided a link to google drive, then the *Show more photos* button will appear, which will redirect to the resource;"
                }
            },
			{
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": ":black_small_square: Anyone in the usergroup #techops can change the price and mark the item as sold;"
                }
            },
			{
        	    "type": "section",
        	    "text": {
        	      "type": "mrkdwn",
        	      "text": ":black_small_square: When the price changes, the old ad is deleted along with the thread;"
        	    }
        	},
        ]
    }
    return view


def get_message_blocks() -> List:
    blocks: List = [
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":information_source: How to create an ad: \n:black_small_square: Upload preview photo from your computer; \n:black_small_square: Press button *Create an advertisement*;\n:black_small_square: Fill and submit the specification; \n :white_small_square: To create an add without preview photo just enter the command */post*"
			}
		}
	]
    return blocks

def get_ad_confirmation_blocks(file_id) -> List:
    blocks: List = [
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": " Create an advertisement",
					},
					"style": "primary",
					"action_id": BUTTON_ACTION_IDS.CREATE_ADVERTISMENT,
                    "value": file_id
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Revoke",
					},
					"style": "danger",
					"action_id": BUTTON_ACTION_IDS.DELETE_PREVIEW_IMAGE,
                    "value": file_id
				}
			]
		}
	]
    return blocks


def get_stuff_specification_view(image_url: str=None):
    view: Dict = {
        "callback_id": VIEW_IDS.ITEM_SPECIFICATION,
	    "title": {
            "type": "plain_text",
            "text": "Lot info"
        },
	    "submit": {
            "type": "plain_text",
            "text": "Submit"
        },
        "type": "modal",
        "close": {
	        "type": "plain_text",
	        "text": "Cancel"
	    },
	    "blocks": [
			{
	          	"type": "input",
	          	"element": {
	          		"type": "plain_text_input",
	          		"placeholder": {
	          			"type": "plain_text",
	          			"text": "Apple iMac 27-Inch Core i7 4.0 (5K, Late 2015)"
	          	    },
					"action_id": INPUT_ACTION_IDS.POST_TOPIC
	          	},
	          	"label": {
	          		"type": "plain_text",
	          		"text": "Topic"
	          	},
				"block_id": BLOCK_IDS.INPUT_POST_TOPIC
	        },
	        {
	        	"type": "input",
	        	"element": {
	        		"type": "plain_text_input",
	        		"placeholder": {
	        			"type": "plain_text",
	        			"text": "https://slack-files.com/"
	        	    },
			        "action_id": INPUT_ACTION_IDS.PREVIEW_ITEM_IMAGE_URL,
                    "initial_value": image_url or ""
	            },
	         	"label": {
	         		"type": "plain_text",
	           		"text": "Preview image URL"
	           	},
				"optional": True,
				"block_id": BLOCK_IDS.INPUT_PREVIEW_ITEM_IMAGE_URL
	        },
			{
	        	"type": "input",
	        	"element": {
	        		"type": "plain_text_input",
	        		"placeholder": {
	        			"type": "plain_text",
	        			"text": "https://slack-files.com/"
	        	    },
			        "action_id": INPUT_ACTION_IDS.MORE_ITEM_IMAGES_URL
	            },
	         	"label": {
	         		"type": "plain_text",
	           		"text": "More photos by URL"
	           	},
				"optional": True,
				"block_id": BLOCK_IDS.INPUT_MORE_ITEM_IMAGES_URL
	        },
	        {
	           	"type": "input",
	            "element": {
	            	"type": "plain_text_input",
	            	"placeholder": {
	            		"type": "plain_text",
	            		"text": "€"
	            	},
					"action_id": INPUT_ACTION_IDS.ITEM_PRICE
	            },
	            "label": {
	            	"type": "plain_text",
	            	"text": "Price"
	            },
				"block_id": BLOCK_IDS.INPUT_ITEM_PRICE
	        },
	        {
	            "type": "input",
	            "element": {
	            	"type": "static_select",
	            	"placeholder": {
	            		"type": "plain_text",
	            		"text": "Choose condition"
	            	},
	            	"options": [
	            		{
	            			"text": {
	            				"type": "plain_text",
	            				"text": "Has deep scratches and/or missing some minor part"
	            			},
	            			"value": "Has deep scratches and/or missing some minor part"
	            		},
	            		{
	            			"text": {
	            				"type": "plain_text",
	            				"text": "Minor, but multiple cosmetic issues"
	            			},
	            			"value": "Minor, but multiple cosmetic issues"
	            		},
	            		{
	            			"text": {
	            				"type": "plain_text",
	            				"text": "Minor cosmetic issues, hardly noticeable"
	            			},
	            			"value": "Minor cosmetic issues, hardly noticeable"
	            		},
	            		{
	            			"text": {
	            				"type": "plain_text",
	            				"text": "Good condition with hardly any visible cosmetic issues"
	            			},
	            			"value": "Good condition with hardly any visible cosmetic issues"
	            		},
	            			{
	            				"text": {
	            					"type": "plain_text",
	            					"text": "Mint condition"
	            				},
	            				"value": "Mint condition"
	            			}
	            		],
	            		"action_id": INPUT_ACTION_IDS.ITEM_CONDITION,
	            	},
	            		"label": {
	            			"type": "plain_text",
	            			"text": "Item condition"
	            		},
						"block_id": BLOCK_IDS.SELECT_ITEM_CONDITION
	            	},
	            	{
	            		"type": "input",
	            		"element": {
	            			"type": "plain_text_input",
	            			"multiline": True,
	            			"placeholder": {
	            				"type": "plain_text",
	            				"text": "Screen size: 27''\nProcessor: Intel Core i5  4.8 GHz\nRAM: 8GB DDR4\nGraphics: Radeon Pro 5300\nStorage:  512 GB/SSD"
	            			},
							"action_id": INPUT_ACTION_IDS.ITEM_DESCRIPTION,
	            		},
	            		"label": {
	            			"type": "plain_text",
	            			"text": "Description"
	            		},
						"block_id": BLOCK_IDS.INPUT_ITEM_DESCRIPTION
	            	},
	            ]
            }

    return view


def get_item_ad_blocks(
	topic: str, 
	image_url: Optional[str],
	more_images_url: Optional[str],
	description: str, 
	price: str, 
	item_condition: str,
	sold: bool=False
	) -> List:

	admin_buttons_block: Dict = {
		"type": "actions",
		"elements": [
			{
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Mark as sold"
				},
				"action_id": BUTTON_ACTION_IDS.MARK_SOLD
			},
			{
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Change price"
				},
				"action_id": BUTTON_ACTION_IDS.CHANGE_PRICE
			}
		],
		"block_id": BLOCK_IDS.AD_ADMIN_ACTION_BUTTONS
	}

	topic_block: Dict =	{
		"type": "header",
		'block_id': BLOCK_IDS.AD_TOPIC,
		"text": {
			"type": "plain_text",
			"text": topic
		}
	}

	description_block: Dict = {
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": f"{AD_VIEW_INDENTS.DESCRIPTION}\n{description}"
		},
		"block_id": BLOCK_IDS.AD_ITEM_DESCRIPTION
	}

	price_block: Dict = {
		"type": "header",
		"text": {
			"type": "plain_text",
			"text": f"{AD_VIEW_INDENTS.PRICE}: {price} €"
		},
		"block_id": BLOCK_IDS.AD_ITEM_PRICE
	}

	item_conditions_block: Dict = {
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": f"{AD_VIEW_INDENTS.CONDITION}\n{item_condition}"
		},
		"block_id": BLOCK_IDS.AD_ITEM_CONDITION
	}

	sale_condition_block: Dict = {
		"type": "context",
		"elements": [
			{
				"type": "plain_text",
				"text": "Cash payments only. Returns are not accepted",
			}
		],
		"block_id": BLOCK_IDS.AD_SALE_CONDITION
	}

	user_buttons_block_elements: List = [
		{
			"type": "button",
			"text": {
				"type": "plain_text",
				"text": "I want to buy"
			},
			"style": "primary",
			"action_id": BUTTON_ACTION_IDS.BUY_ITEM
		}
	]

	if more_images_url is not None:
		user_buttons_block_elements.append({
			"type": "button",
			"text": {
				"type": "plain_text",
				"text": "Show more photos"
			},
			"style": "danger",
			"action_id": BUTTON_ACTION_IDS.SHOW_MORE_ITEM_PHOTOS,
			"url": more_images_url
		})

	user_buttons_block: Dict = {
		"type": "actions",
		"elements": user_buttons_block_elements,
		"block_id": BLOCK_IDS.AD_USER_ACTION_BUTTONS
	}

	post: List[Dict] = [topic_block]
	post.append(admin_buttons_block)
	if image_url is not None and not sold:
		image_block: Dict = {
			"type": "image",
			"image_url": image_url,
			"alt_text": "inspiration",
			"block_id": BLOCK_IDS.AD_ITEM_PREVIEW_IMAGE
		}
		post.append(image_block)

	post.append(description_block)
	post.append(item_conditions_block)
	post.append(price_block)
	post.append(sale_condition_block)
	post.append(user_buttons_block)
	return post


def change_item_price_view(message_ts: str, channel_id: str) -> Dict:
	new_price_view: Dict = {
		"callback_id": VIEW_IDS.INPUT_NEW_ITEM_PRICE,
		"type": "modal",
		"title": {
			"type": "plain_text",
			"text": "Change lot price"
		},
		"submit": {
			"type": "plain_text",
			"text": "Submit"
		},
		"close": {
			"type": "plain_text",
			"text": "Cancel"
		},
		"blocks": [
		{
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"action_id": "plain_text_input-action",
				"placeholder": {
					"type": "plain_text",
					"text": "Enter new price"
				}
			},
			"label": {
				"type": "plain_text",
				"text": "Item price:"
				},
			"block_id": BLOCK_IDS.INPUT_NEW_ITEM_PRICE
		},
		{
			"type": "context",
			"block_id": BLOCK_IDS.MESSAGE_TS_CONTEXT,
			"elements": [
				{
					"type": "plain_text",
					"text": message_ts
				}
			]
		},
		{
			"type": "context",
			"block_id": BLOCK_IDS.CHANNEL_ID_CONTEXT,
			"elements": [
				{
					"type": "plain_text",
					"text": channel_id
				}
			]
		}
	]
	}
	return new_price_view