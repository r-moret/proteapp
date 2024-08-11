import {
  EditInformSchema,
  InformInfoSchema,
  InformSchema,
  UserInfoSchema,
  UserSchema
} from './declarations'

export const InformAdapter = (input: any) => InformSchema.parse(input)
export const InformInfoAdapter = (input: any) => InformInfoSchema.parse(input)
export const EditInformAdapter = (input: any) => EditInformSchema.parse(input)
export const UserAdapter = (input: any) => UserSchema.parse(input)
export const UserInfoAdapter = (input: any) => UserInfoSchema.parse(input)
