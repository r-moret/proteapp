import { z } from 'zod'

export const YardSchema = z.object({
  id: z.number(),
  name: z.string()
})

export const AppointmentSchema = z.object({
  id: z.number(),
  date: z.coerce.date(),
  description: z.string(),
  is_past: z.boolean()
})

export const TreatmentSchema = z.object({
  id: z.number(),
  name: z.string(),
  zone: z.string().nullish(),
  frequency: z.number().nullish(),
  final_date: z.coerce.date().nullish(),
  amount: z.string().nullish()
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
  treatments: z.array(TreatmentSchema).nullish(),
  appointments: z.array(AppointmentSchema).nullish()
})

export type Yard = z.infer<typeof YardSchema>
export type Treatment = z.infer<typeof TreatmentSchema>
export type Appointment = z.infer<typeof AppointmentSchema>
export type Animal = z.infer<typeof AnimalSchema>
