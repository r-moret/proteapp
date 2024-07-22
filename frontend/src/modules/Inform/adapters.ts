import { UserInfoSchema, UserSchema } from './declarations'

export const UserAdapter = (input: any) => UserSchema.parse(input)
export const UserInfoAdapter = (input: any) => UserInfoSchema.parse(input)
