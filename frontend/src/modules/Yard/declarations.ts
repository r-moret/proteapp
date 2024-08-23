import { z } from 'zod'

const IdSchema = z.string().ulid()

export const YardInfoSchema = z.object({
  id: IdSchema,
  name: z.string()
})

export const YardSchema = YardInfoSchema.extend({
  animals: z.array(
    z.object({
      id: IdSchema,
      name: z.string()
    })
  )
})

export const EditYardSchema = z.object({
  name: z.string().min(1)
})

export const EditYardOrderSchema = z.object({
  date: z.coerce.date(),
  yardOrder: z.array(IdSchema)
})

export const YardOrderSchema = z.object({
  id: IdSchema,
  date: z.coerce.date(),
  yardOrder: z.array(
    z.object({
      id: IdSchema,
      name: z.string()
    })
  )
})

export type EditYardOrder = z.infer<typeof EditYardOrderSchema>
export type YardOrder = z.infer<typeof YardOrderSchema>
export type YardInfo = z.infer<typeof YardInfoSchema>
export type Yard = z.infer<typeof YardSchema>
export type EditYard = z.infer<typeof EditYardSchema>
