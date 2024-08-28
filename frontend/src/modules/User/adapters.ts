import { UserInfoSchema, EditUserSchema, UserSchema, EnrichedEditUserSchema } from './declarations'
import { ImageAdapter } from '@/utils'

export const EditUserAdapter = (input: any) => EditUserSchema.parse(input)
export const EnrichedEditUserAdapter = (input: any) => EnrichedEditUserSchema.parse(input)

export const UserInfoAdapter = (input: any) => ImageAdapter(UserInfoSchema.parse(input))
export const UserAdapter = (input: any) => ImageAdapter(UserSchema.parse(input))
