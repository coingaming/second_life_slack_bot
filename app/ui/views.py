from typing import List, Dict
from marshmallow import Schema, fields


#------------------------------------------------
class DescriptionSchema(Schema):
	type: fields.Str = fields.Str(required=True)
	text: fields.Str = fields.Str(required=True)
	emoji: fields.Bool = fields.Bool(required=True)

class Description:
	type: str
	text: str
	emoji: bool
	schema_class: DescriptionSchema = DescriptionSchema

	def __init__(self, type: str="plain_text", text: str="", emoji: bool=True):
		self.type = type
		self.text = text
		self.emoji = emoji

	def dump(self):
		return self.schema_class().dump(self)

#------------------------------------------------
class Option:
	text: Description
	value: str

	def __init__(self, text: Description, value: str):
		self.text = text
		self.value = value


class OptionSchema(Schema):
	text: DescriptionSchema = fields.Nested(DescriptionSchema, required=True)
	value: fields.Str = fields.Str(required=True)

#------------------------------------------------
class Element:
	type: str
	action_id: str
	options: List[Option] # optional
	placeholder: Description # optional

	def __init__(
		self, 
		type, 
		action_id, 
		options=None, 
		placeholder=None
	):
		self.type = type
		self.action_id = action_id

		if options is not None:
			self.options = options

		if placeholder is not None:
			self.placeholder = placeholder

class ElementSchema(Schema):
	type: fields.Str = fields.Str()
	action_id: fields.Str = fields.Str()
	options: fields.Nested = fields.Nested(OptionSchema, many=True) # optional
	placeholder: fields.Nested = fields.Nested(DescriptionSchema) # optional

#------------------------------------------------
class Block:
	type: str
	label: Description
	element: Element

	def __init__(self, label, element, type="input") -> None:
		self.type = type
		self.label = label
		self.element = element

class BlockSchema(Schema):
	type: fields.Str = fields.Str()
	label: fields.Nested = fields.Nested(DescriptionSchema)
	element: fields.Nested = fields.Nested(ElementSchema)

#------------------------------------------------
class DeviceForExistingStaffPayload:
	user: str
	team: str
	approvers: List[str]
	device_specifics: str
	reason_for_request: str

	def __init__(self, user, team, approvers, device_specifics, reason):
		self.user = user
		self.team = team
		self.approvers = approvers
		self.device_specifics = device_specifics
		self.reason_for_request = reason

	@classmethod
	def load(cls, raw_data: Dict) -> "DeviceForExistingStaffPayload":
		view_data = raw_data['view']
		state = view_data['state']
		values = state['values']

		for block in values.items():
			print('???? block id: ', block)

		#print('>>> try to load data: ', raw_data['view']['state']['values'])

	@classmethod
	def dump(cls) -> Dict:
		pass

class DeviceForExistingStaffPayloadSchema(Schema):
	user: fields.Str = fields.Str()
	team: fields.Str = fields.Str()
	approvers: fields.List = fields.List(fields.Str)
	device_specifics: fields.Str = fields.Str()
	reason_for_request: fields.Str = fields.Str()


#------------------------------------------------

class DeviceForExistingStaffViewSchema(Schema):
	type: fields.Str = fields.Str()
	callback_id: fields.Str = fields.Str()
	title: fields.Nested = fields.Nested(DescriptionSchema)
	submit: fields.Nested = fields.Nested(DescriptionSchema)
	close: fields.Nested = fields.Nested(DescriptionSchema)
	blocks: fields.Nested = fields.Nested(BlockSchema, many=True)


class DeviceForExistingStaffView:
	type: str = "modal"
	callback_id: str
	title: Description
	submit: Description
	close: Description
	blocks: List[Block]


	def __init__(
		self, 
		callback_id, 
		title,
		blocks, 
		submit, 
		close
	):
		self.callback_id = callback_id
		self.title = title
		self.blocks = blocks
		self.submit = submit
		self.close = close

	@classmethod
	def dump(cls) -> Dict:
		blocks = [
			# user email address text input field
			Block(
				label=Description(text="User Email Address"),
				element=Element(
					type="plain_text_input",
					action_id="user_email_device_for_existing_staff_action_id",
					placeholder=Description(text="Enter email address")
				)
			),

			# team static select field
			Block(
				label=Description(text="Team/Division"),
				element=Element(
					type="static_select",
					action_id="team_division_device_for_existing_staff_action_id",
					options=[
						Option(text=Description(text="Accounting"), value="Accounting"),
						Option(text=Description(text="BI"), value="BI"),
						Option(text=Description(text="Bombay Live Product"), value="Bombay Live Product"),
						Option(text=Description(text="Hub88"), value="Hub88"),
						Option(text=Description(text="People"), value="People"),
					],
					placeholder=Description(text="Select team or division")
				)
			),

			# team static select field
			Block(
				label=Description(text="Manager/Approvals"),
				element=Element(
					type="multi_static_select",
					action_id="approvals_device_for_existing_staff_action_id",
					options=[
						Option(text=Description(text="Ian Michailov"), value="Ian Michailov"),
						Option(text=Description(text="Indrek Truu"), value="Indrek Truu"),
					],
					placeholder=Description(text="Select approvals")
				)
			),

			# device specific text input field
			Block(
				label=Description(text="Device Specifics"),
				element=Element(
					type="plain_text_input",
					action_id="device_specifics_device_for_existing_staff_action_id",
					placeholder=Description(text="Enter device specifics")
				)
			),

			# reason for the request
			Block(
				label=Description(text="Reason"),
				element=Element(
					type="plain_text_input",
					action_id="reason_device_for_existing_staff_action_id",
					placeholder=Description(text="Enter reason for the request")
				)
			),
		]

		view: "DeviceForExistingStaffView" = cls(
			callback_id="device_for_existing_staff_view",
			title=Description(text="Existing staff"),
			blocks=blocks,
			submit=Description(text="Submit"),
			close=Description(text="Cancel")
		)

		return DeviceForExistingStaffViewSchema().dump(view)

