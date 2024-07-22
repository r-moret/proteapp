import { z } from 'zod'

export const UserInfoSchema = z.object({
  id: z.string().ulid(),
  person: z.object({
    name: z.string(),
    email: z.string(),
    firstSurname: z.string(),
    secondSurname: z.string().nullish()
  }),
  active: z.boolean(),
  veteran: z.boolean(),
  image: z.string().nullish()
})

export const UserSchema = UserInfoSchema.extend({
  person: z.object({
    name: z.string(),
    email: z.string(),
    firstSurname: z.string(),
    phone: z.string().refine((phone) => /^\+[1-9]\d{1,14}$/.test(phone)), // TODO: This regex can be improved
    secondSurname: z.string().nullish()
  })
})

export type User = z.infer<typeof UserSchema>
export type UserInfo = z.infer<typeof UserInfoSchema>
