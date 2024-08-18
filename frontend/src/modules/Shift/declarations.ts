import { z } from 'zod'
import { IdSchema, type UserInfo } from '../Inform/declarations'
import { createObjectSchema } from '@/utils'

export const ShiftStatusSchema = z.object({
  status: z.enum(['open', 'closed'])
})

const ShiftTimeSchema = z.enum(['morning', 'afternoon'])
const WeekDaySchema = z.enum([
  'monday',
  'thursday',
  'wednesday',
  'tuesday',
  'friday',
  'saturday',
  'sunday'
])

export const ShiftActionSchema = z.object({
  type: z.enum(['add_user', 'remove_user']),
  user: IdSchema,
  shift: z.object({
    day: WeekDaySchema,
    time: ShiftTimeSchema
  })
})

const ShiftDaySchema = createObjectSchema(ShiftTimeSchema, z.array(IdSchema))
export const ShiftSchema = createObjectSchema(WeekDaySchema, ShiftDaySchema)

export type ShiftStatus = z.infer<typeof ShiftStatusSchema>
export type ShiftAction = z.infer<typeof ShiftActionSchema>
export type ShiftTime = z.infer<typeof ShiftTimeSchema>
export type WeekDay = z.infer<typeof WeekDaySchema>
export type Shift = z.infer<typeof ShiftSchema>

export type EnrichedShiftDay = {
  morning: UserInfo[]
  afternoon: UserInfo[]
}

export type EnrichedShift = Record<WeekDay, EnrichedShiftDay>
