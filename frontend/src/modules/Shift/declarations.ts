import { z } from 'zod'
import { IdSchema, type UserInfo } from '../Inform/declarations'
import { createObjectSchema } from '@/utils'

const ShiftTimeSchema = z.enum(['morning', 'afternoon'])
const ShiftDaySchema = createObjectSchema(ShiftTimeSchema, z.array(IdSchema))
const WeekDaySchema = z.enum([
  'monday',
  'thursday',
  'wednesday',
  'tuesday',
  'friday',
  'saturday',
  'sunday'
])

export const ShiftStatusSchema = z.object({
  status: z.enum(['open', 'closed'])
})

export const ShiftSelectionSchema = z.object({
  day: WeekDaySchema,
  time: ShiftTimeSchema
})

export const ShiftActionSchema = z.object({
  type: z.enum(['add_user', 'remove_user']),
  user: IdSchema,
  shift: ShiftSelectionSchema
})

export const ShiftSchema = z.object({
  connected: z.number(),
  timetable: createObjectSchema(WeekDaySchema, ShiftDaySchema)
})

type ShiftTime = z.infer<typeof ShiftTimeSchema>

export type ShiftStatus = z.infer<typeof ShiftStatusSchema>
export type ShiftSelection = z.infer<typeof ShiftSelectionSchema>
export type ShiftAction = z.infer<typeof ShiftActionSchema>
export type WeekDay = z.infer<typeof WeekDaySchema>
export type Shift = z.infer<typeof ShiftSchema>

export type EnrichedShift = Record<WeekDay, Record<ShiftTime, UserInfo[]>>
