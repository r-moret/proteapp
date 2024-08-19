import { UserInfoSchema, EditUserSchema } from './declarations'

export const UserInfoAdapter = (input: any) => UserInfoSchema.parse(input)
export const EditUserAdapter = (input: any) => EditUserSchema.parse(input)
