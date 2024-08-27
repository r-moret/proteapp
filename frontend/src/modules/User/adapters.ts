import { UserInfoSchema, EditUserSchema, UserSchema, EnrichedEditUserSchema } from './declarations'

export const EditUserAdapter = (input: any) => EditUserSchema.parse(input)
export const EnrichedEditUserAdapter = (input: any) => EnrichedEditUserSchema.parse(input)

export const UserInfoAdapter = (input: any) => {
  const user = UserInfoSchema.parse(input)

  if (user.image) {
    user.image = `${import.meta.env.VITE_BACKEND_URL}/${user.image}`
  }

  return user
}
export const UserAdapter = (input: any) => {
  const user = UserSchema.parse(input)

  if (user.image) {
    user.image = `${import.meta.env.VITE_BACKEND_URL}/${user.image}`
  }

  return user
}
