import { z } from 'zod'

const IdSchema = z.string().ulid()

export const AdoptionInfoSchema = z.object({
  id: IdSchema,
  registerDate: z.coerce.date(),
  foster: z.boolean(),
  revocationDate: z.coerce.date().nullish(),
  animal: z.object({
    id: IdSchema,
    name: z.string(),
    image: z.string().nullish()
  }),
  person: z.object({
    id: IdSchema,
    name: z.string(),
    firstSurname: z.string()
  })
})

export const AdoptionSchema = z.object({
  id: IdSchema,
  registerDate: z.coerce.date(),
  foster: z.boolean(),
  revocationDate: z.coerce.date().nullish(),
  animal: z.object({
    id: IdSchema,
    name: z.string(),
    image: z.string().nullish(),
    description: z.string().nullish(),
    personality: z.string().nullish(),
    birthDate: z.coerce.date().nullish(),
    isAnimalCompatible: z.boolean().nullish(),
    isCastrated: z.boolean().nullish()
  }),
  person: z.object({
    id: IdSchema,
    name: z.string(),
    firstSurname: z.string(),
    secondSurname: z.string().nullish(),
    email: z.string().nullish(),
    phone: z.string()
  }),
  monitorings: z.array(
    z.object({
      id: IdSchema,
      followDate: z.coerce.date(),
      note: z.string()
    })
  )
})

export const EditAdoptionSchema = z.object({
  registerDate: z.coerce.date(),
  foster: z.boolean(),
  animal: IdSchema,
  person: IdSchema
})

export const EditMonitoringSchema = z.object({
  followDate: z.coerce.date(),
  note: z.string(),
  adoption: IdSchema
})

export type AdoptionInfo = z.infer<typeof AdoptionInfoSchema>
export type Adoption = z.infer<typeof AdoptionSchema>
export type EditMonitoring = z.infer<typeof EditMonitoringSchema>
export type EditAdoption = z.infer<typeof EditAdoptionSchema>
