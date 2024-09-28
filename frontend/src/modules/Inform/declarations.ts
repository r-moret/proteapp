import { z } from 'zod'
import type { AnimalInfo } from '@/modules/Animal/declarations'
import type { UserInfo } from '@/modules/User/declarations'
import { YardInfoSchema, type YardInfo } from '@/modules/Yard/declarations'

export const IdSchema = z.string().ulid()

const TimeSchema = z
  .string()
  .refine((val) =>
    /^(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(Z|[+-](?:2[0-3]|[01][0-9])(?::(?:[0-5][0-9]))?)$/.test(
      val
    )
  )

export const EditInformSchema = z.object({
  creator: IdSchema,
  volunteers: z.array(IdSchema),
  date: z.coerce.date(),
  timeRange: z.object({
    start: TimeSchema,
    end: TimeSchema
  }),
  yardOrder: IdSchema,
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
    start: TimeSchema,
    end: TimeSchema
  })
})

export const InformSchema = InformInfoSchema.extend({
  yardOrder: z.array(YardInfoSchema),
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
  testedAnimals: z
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

export type EditInform = z.infer<typeof EditInformSchema>
export type InformInfo = z.infer<typeof InformInfoSchema>
export type Inform = z.infer<typeof InformSchema>

export type Arrival = { name: string; description?: string | null }
export type AnimaNote = { info: AnimalInfo; note?: string }
export type Visit = { visitor: string; description: string }
export type Adoption = { animal: AnimalInfo; foster: boolean }
export type AnimalTest = { animal: AnimalInfo; compatible: boolean }
export type Loss = { animal: AnimalInfo }
export type TimeRange = [{ hours: number; minutes: number }, { hours: number; minutes: number }]

export type EnrichedFields =
  | ['creator', UserInfo]
  | ['volunteers', UserInfo[]]
  | ['date', Date]
  | ['timeRange', TimeRange]
  | ['highlights', string[] | undefined | null]
  | ['yardOrder', YardInfo[]]
  | ['notes', AnimaNote[] | undefined | null]
  | ['adoptions', Adoption[] | undefined | null]
  | ['testedAnimals', AnimalTest[] | undefined | null]
  | ['losses', Loss[] | undefined | null]
  | ['visits', Visit[] | undefined | null]
  | ['arrivals', Arrival[] | undefined | null]

export type EnrichedInform = {
  [key in EnrichedFields[0]]: Extract<EnrichedFields, [key, any]>[1]
}
