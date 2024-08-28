import { z } from 'zod'
import { YardInfoSchema } from '@/modules/Yard/declarations'

const IdSchema = z.string().ulid()

export const EditAnimalSchema = z.object({
  name: z.string().min(1),
  sex: z.enum(['male', 'female']),
  personality: z.string().nullish(),
  description: z.string().nullish(),
  birthDate: z.coerce.date().nullish(),
  entryDate: z.coerce.date().nullish(),
  isAnimalCompatible: z.boolean().nullish(),
  isCastrated: z.boolean().nullish(),
  image: z.string().nullish(),
  yard: IdSchema.nullish()
})

export const EnrichedEditAnimalSchema = EditAnimalSchema.extend({
  yard: YardInfoSchema.nullish()
})

export const AnimalInfoSchema = z.object({
  id: IdSchema,
  name: z.string(),
  sex: z.enum(['male', 'female']),
  image: z.string().nullish(),
  yard: z
    .object({
      id: IdSchema,
      name: z.string()
    })
    .nullish(),
  birthDate: z.coerce.date().nullish(),
  isAnimalCompatible: z.boolean().nullish(),
  isCastrated: z.boolean().nullish(),
  treatments: z.array(
    z.object({
      id: IdSchema,
      name: z.string()
    })
  )
})

export const AnimalSchema = AnimalInfoSchema.extend({
  personality: z.string().nullish(),
  description: z.string().nullish(),
  entryDate: z.coerce.date().nullish(),
  treatments: z.array(
    z.object({
      id: IdSchema,
      name: z.string(),
      zone: z.string().nullish(),
      frequency: z.number().nullish(),
      endDate: z.coerce.date().nullish(),
      amount: z.string().nullish()
    })
  ),
  appointments: z.array(
    z.object({
      id: IdSchema,
      date: z.coerce.date(),
      description: z.string(),
      isPast: z.boolean()
    })
  )
})

export const EditTreatmentSchema = z.object({
  name: z.string().min(1),
  zone: z.string().min(1).nullish(),
  frequency: z.number().nullish(),
  endDate: z.coerce.date().nullish(),
  amount: z.string().min(1).nullish(),
  animal: IdSchema
})

export const EditAppointmentSchema = z.object({
  date: z.coerce.date(),
  description: z.string().min(1),
  animal: IdSchema
})

export type EditTreatment = z.infer<typeof EditTreatmentSchema>
export type EditAppointment = z.infer<typeof EditAppointmentSchema>
export type EditAnimal = z.infer<typeof EditAnimalSchema>
export type EnrichedEditAnimal = z.infer<typeof EnrichedEditAnimalSchema>
export type AnimalInfo = z.infer<typeof AnimalInfoSchema>
export type Animal = z.infer<typeof AnimalSchema>
