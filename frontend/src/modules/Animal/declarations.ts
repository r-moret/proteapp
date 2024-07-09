import { z } from 'zod'

export const YardSchema = z.object({
  id: z.number(),
  name: z.string()
})

export const TreatmentSchema = z.object({
  id: z.number(),
  name: z.string(),
  zone: z
    .string()
    .nullable()
    .optional()
    .transform((x) => x ?? undefined),
  frequency: z
    .number()
    .nullable()
    .optional()
    .transform((x) => x ?? undefined)
})

export const AnimalSchema = z.object({
  id: z.number(),
  name: z.string(),
  personality: z.string(),
  description: z.string(),
  sex: z.enum(['female', 'male']),
  birthDate: z.coerce.date(),
  entryDate: z.coerce.date(),
  yard: YardSchema,
  isAnimalCompatible: z.boolean(),
  isCastrated: z.boolean(),
  image: z
    .string()
    .nullable()
    .optional()
    .transform((x) => x ?? undefined),
  treatments: z.array(TreatmentSchema)
})

export type Yard = z.infer<typeof YardSchema>
export type Treatment = z.infer<typeof TreatmentSchema>
export type Animal = z.infer<typeof AnimalSchema>
