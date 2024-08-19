import { z } from 'zod'
const IdSchema = z.string().ulid()
const FileSchema = z.instanceof(File)

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

export const EditUserSchema = z.object({
  person: IdSchema,
  active: z.boolean(),
  veteran: z.boolean(),
  image: FileSchema.nullish(),
  password: z.string()
})

export type UserInfo = z.infer<typeof UserInfoSchema>
export type EditUser = z.infer<typeof EditUserSchema>
