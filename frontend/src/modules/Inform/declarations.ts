import { z } from 'zod'

export const IdSchema = z.string().ulid()

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

export const EditInformSchema = z.object({
  creator: IdSchema,
  volunteers: z.array(IdSchema),
  date: z.coerce.date(),
  timeRange: z.object({
    start: z.object({ hours: z.number(), minutes: z.number() }),
    end: z.object({ hours: z.number(), minutes: z.number() })
  }),
  notes: z.array(
    z.object({
      animal: IdSchema,
      text: z.string().min(1)
    })
  ),
  highlights: z.array(z.string()).nullish(),
  visits: z.array(
    z.object({
      visitor: z.string().min(1),
      description: z.string().min(1)
    })
  ),
  arrivals: z.array(
    z.object({
      name: z.string().min(1),
      description: z.string().min(1).nullish()
    })
  ),
  losses: z.array(
    z.object({
      animal: IdSchema
    })
  ),
  adoptions: z.array(
    z.object({
      animal: IdSchema,
      foster: z.boolean()
    })
  ),
  testedAnimals: z.array(
    z.object({
      animal: IdSchema,
      compatible: z.boolean()
    })
  )
})

export const InformInfoSchema = z.object({
  id: IdSchema,
  creator: z.object({
    id: IdSchema,
    person: z.object({
      name: z.string(),
      firstSurname: z.string(),
      secondSurname: z.string().nullish()
    })
  }),
  volunteers: z.array(
    z.object({
      id: IdSchema,
      person: z.object({
        name: z.string(),
        firstSurname: z.string(),
        secondSurname: z.string().nullish()
      })
    })
  ),
  date: z.coerce.date(),
  timeRange: z.object({
    start: z.object({ hours: z.number(), minutes: z.number() }),
    end: z.object({ hours: z.number(), minutes: z.number() })
  })
})

export const InformSchema = InformInfoSchema.extend({
  notes: z.array(
    z.object({
      yard: z
        .object({
          id: IdSchema,
          name: z.string()
        })
        .nullish(),
      animal: z.object({
        id: IdSchema,
        name: z.string()
      }),
      text: z.string().min(1)
    })
  ),
  highlights: z.array(z.string()).nullish(),
  visits: z
    .array(
      z.object({
        visitor: z.string().min(1),
        description: z.string().min(1)
      })
    )
    .nullish(),
  arrivals: z
    .array(
      z.object({
        name: z.string().min(1),
        description: z.string().min(1).nullish()
      })
    )
    .nullish(),
  losses: z
    .array(
      z.object({
        animal: z.object({
          id: IdSchema,
          name: z.string()
        })
      })
    )
    .nullish(),
  adoptions: z
    .array(
      z.object({
        animal: z.object({
          id: IdSchema,
          name: z.string()
        }),
        foster: z.boolean()
      })
    )
    .nullish(),
  tested_animals: z
    .array(
      z.object({
        animal: z.object({
          id: IdSchema,
          name: z.string()
        }),
        compatible: z.boolean()
      })
    )
    .nullish()
})

export type User = z.infer<typeof UserSchema>
export type UserInfo = z.infer<typeof UserInfoSchema>
export type EditInform = z.infer<typeof EditInformSchema>
export type InformInfo = z.infer<typeof InformInfoSchema>
export type Inform = z.infer<typeof InformSchema>
