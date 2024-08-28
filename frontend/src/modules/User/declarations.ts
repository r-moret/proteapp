import { z } from 'zod'
import { PersonSchema } from '../Person/declarations'
const IdSchema = z.string().ulid()

export const UserInfoSchema = z.object({
  id: IdSchema,
  person: z.object({
    id: IdSchema,
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
    id: IdSchema,
    name: z.string(),
    email: z.string(),
    firstSurname: z.string(),
    phone: z.string(),
    secondSurname: z.string().nullish()
  })
})

export const EditUserSchema = z.object({
  person: IdSchema,
  active: z.boolean(),
  veteran: z.boolean(),
  image: z.string().nullish()
})

export const EnrichedEditUserSchema = EditUserSchema.extend({
  person: PersonSchema
})

export type User = z.infer<typeof UserSchema>
export type UserInfo = z.infer<typeof UserInfoSchema>
export type EditUser = z.infer<typeof EditUserSchema>
export type EnrichedEditUser = z.infer<typeof EnrichedEditUserSchema>
