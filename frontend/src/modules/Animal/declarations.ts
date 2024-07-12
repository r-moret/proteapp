import { z } from 'zod'

export const YardSchema = z.object({
  id: z.number(),
  name: z.string()
})

export const TreatmentSchema = z.object({
  id: z.number().nullish(),
  name: z.string(),
  zone: z.string().nullish(),
  frequency: z.number().nullish(),
  amount: z.string().nullish(),
  endDate: z.coerce.date().nullish()
})

export const AnimalSchema = z.object({
  id: z.number(),
  name: z.string(),
  personality: z.string().nullish(),
  description: z.string().nullish(),
  sex: z.enum(['female', 'male']),
  birthDate: z.coerce.date().nullish(),
  entryDate: z.coerce.date().nullish(),
  yard: YardSchema.nullish(),
  isAnimalCompatible: z.boolean().nullish(),
  isCastrated: z.boolean().nullish(),
  image: z.string().nullish(),
  treatments: z.array(TreatmentSchema).nullish()
})

export type Yard = z.infer<typeof YardSchema>
export type Treatment = z.infer<typeof TreatmentSchema>
export type Animal = z.infer<typeof AnimalSchema>
