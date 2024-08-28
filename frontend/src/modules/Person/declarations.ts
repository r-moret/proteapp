import { z } from 'zod'

const IdSchema = z.string().ulid()

export const PersonInfoSchema = z.object({
  id: IdSchema,
  name: z.string(),
  firstSurname: z.string(),
  secondSurname: z.string().nullish(),
  email: z.string()
})

export const PersonSchema = z.object({
  id: IdSchema,
  name: z.string(),
  firstSurname: z.string(),
  phone: z.string(),
  secondSurname: z.string().nullish(),
  email: z.string()
})

export const EditPersonSchema = z.object({
  name: z.string().min(1),
  firstSurname: z.string().min(1),
  phone: z.string().min(1),
  secondSurname: z.string().min(1).nullish(),
  email: z.string().min(1)
})

export type Person = z.infer<typeof PersonSchema>
export type PersonInfo = z.infer<typeof PersonInfoSchema>
export type EditPerson = z.infer<typeof EditPersonSchema>
